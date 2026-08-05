
import hmf_djerba.plugins.hmf.genomic_landscape.constants as constants
from djerba.util.html import html_builder as hb
from markdown import markdown
from string import Template
from djerba.util.logger import logger

class html_builder:
    
    def assemble_biomarker_plot(self,biomarker,plot):
        template='<img id="{0}" style="width: 100%; " src="{1}"'
        cell = template.format(biomarker,plot)
        return(cell)

    def biomarker_table_rows(self, biomarkers, can_report_hrd, cant_report_hrd_reason):
        rows = []
        for marker, info in biomarkers.items():
            if marker == "HRD" and not can_report_hrd:
                if cant_report_hrd_reason == constants.CHORD_REASON:
                    # CHORD could not make a call, so there is no score or plot to show
                    text = "HRD score could not be determined (reason: {0}).".format(
                        info[constants.METRIC_TEXT]
                    )
                else:
                    # evaluate_reportability() in the plugin can only ever set
                    # CHORD_REASON, so any other value means the plugin and this
                    # renderer have gone out of sync
                    msg = "Unexpected reason for not reporting HRD: '{0}'".format(
                        cant_report_hrd_reason
                    )
                    raise ValueError(msg)
                cells = [
                    hb.td(info[constants.ALT]),
                    hb.td("NA"),
                    hb.td(text)
                ]

            elif marker == "MSI" and info[constants.METRIC_ALTERATION] == "UNKNOWN":
                cells = [
                    hb.td(info[constants.ALT]),
                    hb.td("UNKNOWN"),
                    hb.td("Microsatellite status could not be determined, as no somatic variants were detected")
                ]

            else:
                cells = [
                    hb.td(info[constants.ALT]),
                    hb.td(info[constants.METRIC_ALTERATION]),
                    hb.td(self.assemble_biomarker_plot(info[constants.ALT], info[constants.METRIC_PLOT]))
                ]
            rows.append(hb.table_row(cells))
        return rows
