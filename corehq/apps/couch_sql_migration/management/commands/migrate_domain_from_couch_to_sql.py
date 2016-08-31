from itertools import izip_longest
from optparse import make_option

from django.core.management.base import CommandError, LabelCommand

from corehq.apps.couch_sql_migration.couchsqlmigration import do_couch_to_sql_migration, delete_diff_db
from corehq.apps.domain.dbaccessors import get_doc_ids_in_domain_by_type
from corehq.apps.hqcase.dbaccessors import get_case_ids_in_domain
from corehq.form_processor.backends.sql.dbaccessors import FormAccessorSQL, CaseAccessorSQL
from corehq.form_processor.models import XFormInstanceSQL
from corehq.form_processor.utils import should_use_sql_backend
from couchforms.dbaccessors import get_form_ids_by_type
from couchforms.models import doc_types, XFormInstance


class Command(LabelCommand):
    args = "<domain>"
    option_list = LabelCommand.option_list + (
        make_option('--MIGRATE', action='store_true', default=False),
        make_option('--blow_away', action='store_true', default=False),
        make_option('--stats', action='store_true', default=False),
    )

    @staticmethod
    def require_only_option(sole_option, options):
        base_options = {option.dest for option in LabelCommand.option_list}
        assert all(not value for key, value in options.items()
                   if key not in base_options and key != sole_option)

    def handle_label(self, domain, **options):
        if should_use_sql_backend(domain):
            raise CommandError(u'It looks like {} has already been migrated.'.format(domain))

        if options['MIGRATE']:
            self.require_only_option('MIGRATE', options)
            do_couch_to_sql_migration(domain)
        if options['blow_away']:
            self.require_only_option('blow_away', options)
            _confirm(
                "This will delete all SQL forms and cases for the domain {}. "
                "Are you sure you want to continue?".format(domain)
            )
            _blow_away_migration(domain)
        if options['stats']:
            self.print_stats(domain)

    def print_stats(self, domain):
        for doc_type in doc_types():
            form_ids_in_couch = set(get_form_ids_by_type(domain, doc_type))
            form_ids_in_sql = set(FormAccessorSQL.get_form_ids_in_domain_by_type(domain, doc_type))
            self._print_status(doc_type, form_ids_in_couch, form_ids_in_sql)

        form_ids_in_couch = set(get_doc_ids_in_domain_by_type(domain, "XFormInstance-Deleted", XFormInstance.get_db()))
        form_ids_in_sql = set(FormAccessorSQL.get_deleted_form_ids_in_domain(domain))
        self._print_status("XFormInstance-Deleted", form_ids_in_couch, form_ids_in_sql)

        case_ids_in_couch = set(get_case_ids_in_domain(domain))
        case_ids_in_sql = set(CaseAccessorSQL.get_case_ids_in_domain(domain))
        self._print_status('CommCareCase', case_ids_in_couch, case_ids_in_sql)

        case_ids_in_couch = set(get_doc_ids_in_domain_by_type(domain, "CommCareCase-Deleted", XFormInstance.get_db()))
        case_ids_in_sql = set(CaseAccessorSQL.get_deleted_case_ids_in_domain(domain))
        self._print_status('CommCareCase-Deleted', case_ids_in_couch, case_ids_in_sql)

    def _print_status(self, name, ids_in_couch, ids_in_sql):
        header = ((82 - len(name)) / 2) * '_'
        print '\n{} {} {}'.format(header, name, header)
        row = "{:^40} | {:^40}"
        print row.format('Couch', 'SQL')
        print row.format(len(ids_in_couch), len(ids_in_sql))
        if ids_in_couch ^ ids_in_sql:
            couch_only = list(ids_in_couch - ids_in_sql)
            sql_only = list(ids_in_sql - ids_in_couch)
            for couch, sql in izip_longest(couch_only, sql_only):
                print row.format(couch or '', sql or '')


def _confirm(message):
    if raw_input(
            '{} [y/n]'.format(message)
    ).lower() == 'y':
        return
    else:
        raise CommandError('abort')


def _blow_away_migration(domain):
    assert not should_use_sql_backend(domain)
    delete_diff_db(domain)

    for doc_type in doc_types():
        sql_form_ids = FormAccessorSQL.get_form_ids_in_domain_by_type(domain, doc_type)
        FormAccessorSQL.hard_delete_forms(domain, sql_form_ids)

    sql_form_ids = FormAccessorSQL.get_deleted_form_ids_in_domain(domain)
    FormAccessorSQL.hard_delete_forms(domain, sql_form_ids)

    sql_case_ids = CaseAccessorSQL.get_case_ids_in_domain(domain)
    CaseAccessorSQL.hard_delete_cases(domain, sql_case_ids)

    sql_case_ids = CaseAccessorSQL.get_deleted_case_ids_in_domain(domain)
    CaseAccessorSQL.hard_delete_cases(domain, sql_case_ids)
