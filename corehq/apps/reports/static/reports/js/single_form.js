/* globals Clipboard */
/*
    Interactivity for a single form. Used on the list of forms in the Case History tab when viewing a case, and
    also in the single form view page that's accessible from the submit history report or the "View standalone
    form" button when looking at a form in case history.
*/
hqDefine("reports/js/single_form", function() {
    var initSingleForm = function(options) {
        hqImport("hqwebapp/js/assert_properties").assert(options, ['instance_id', 'form_question_map', 'ordered_question_values'], ['container']);

        var $container = options.container || $("body");

        var initialPageData = hqImport("hqwebapp/js/initial_page_data");
        var analyticsUsage = function(action, callback) {
            var label = 'standalone_form',
                extra = {},
                caseId = initialPageData.get("context_case_id");
            if (caseId) {
                label = 'case';
            }
            hqImport('analytix/js/google').track.event('Edit Data', action, label, '', extra, callback);
        };

        $('.hq-help-template', $container).each(function () {
            hqImport("hqwebapp/js/main").transformHelpTemplate($(this), true);
        });

        $('#edit-form', $container).click(function() {
            analyticsUsage('Edit Form Submission');
        });

        hqImport("reports/js/data_corrections").init($container.find(".data-corrections-trigger"), $container.find(".data-corrections-modal"), {
            properties: options.form_question_map,
            propertyNames: options.ordered_question_values,
            propertyPrefix: "<div class='form-data-question'><i data-bind='attr: { class: icon }'></i> ",
            propertySuffix: "</div>",
            displayProperties: [
                {
                    property: 'label',
                    name: gettext('Labels'),
                },
                {
                    property: 'splitName',
                    name: gettext('Question IDs'),
                    search: 'name',
                },
            ],
            saveUrl: initialPageData.reverse("edit_form", options.instance_id),
        });

        $("#archive-form", $container).submit(function() {
            document.getElementById('archive-form-btn').disabled=true;
            $('#archive-spinner', $container).show();

            // _.after(2,...) means the callback will only be called after *both* analytics
            // functions have finished.
            var analyticsCallback = _.after(2, function() {
                document.getElementById('archive-form').submit();
            });
            analyticsUsage('Archive Form Submission', analyticsCallback);
            hqImport('analytix/js/kissmetrix').track.event("Clicked on Archive Form", {}, analyticsCallback);

            return false;
        });
        $("#unarchive-form", $container).submit(function() {
            document.getElementById('unarchive-form-btn').disabled=true;
            $('#unarchive-spinner', $container).show();
            hqImport('analytix/js/google').track.event('Reports', 'Case History', 'Restore this form', "", {}, function () {
                document.getElementById('unarchive-form').submit();
            });
            return false;
        });
        $("#resave-form", $container).submit(function() {
            document.getElementById('resave-form-btn').disabled=true;
            $('#resave-spinner', $container).show();
        });

        $.when(
            $.getScript(hqImport("hqwebapp/js/initial_page_data").get("clipboardScript"))
        ).done(function () {
            var clipboard = new Clipboard('.copy-xml', { text: function() { return $('#form-xml pre', $container).text(); } }),
                $copyBtn = $('.copy-xml', $container);
            $copyBtn.tooltip({
                title: gettext("Copied!"),
            });
            clipboard.on('success', function() {
                $copyBtn.tooltip('show');
                window.setTimeout(function() { $copyBtn.tooltip('hide'); }, 1000);
            });
        });
    };

    return {
        initSingleForm: initSingleForm,
    };
});
