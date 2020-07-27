from yattag import Doc
from utils.fileutils import get_output_dir
from os import path
import numpy as np
import pandas as pd

def generate_report(stats: dict, simulation_id: str = None) -> str:
    doc, tag, text = Doc().tagtext()
    with tag('html'):
        with tag('body'):
            with tag('h1'):
                text('Simulation Report')

            if simulation_id is not None:
                with tag('p'):
                    text('Simulation id: {}'.format(simulation_id))

            if stats['start'] is not None:
                with tag('p'):
                    text('Start time: {}'.format(stats['start']))
                        
            if stats['stop'] is not None:
                with tag('p'):
                    text('Stop time: {}'.format(stats['stop']))

            with tag('p'):
                text('Signals detected: {}'.format(stats['count']))
            create_signal_type_section(tag, text, 'h2', 'Buy', stats['buy'])
            create_signal_type_section(tag, text, 'h2', 'Sell', stats['sell'])
    report = doc.getvalue()

    output_dir = get_output_dir(simulation_id)
    if not path.exists(output_dir):
        makedirs(output_dir, exist_ok=True)
    output_fp = '{}/report.html'.format(output_dir)
    with open(output_fp, "w") as f:
        f.write(report)


def create_signal_type_section(tag, text, header_tag: str, header: str, stats: dict):
    with tag(header_tag):
        text(header)

    with tag('p'):
        text('Occurrences: {}'.format(stats['count']))
    
    with tag('p'):
        text('Net gain:')
    generate_ul_from_dict(tag, text, stats['net_gain'])

    with tag('p'):
        text('Duration:')
    generate_ul_from_dict(tag, text, stats['duration'])

    with tag('p'):
        text('Position closings:')
    generate_ul_from_dict(tag, text, stats['closings'])


def generate_ul_from_dict(tag, text, content: dict):
    with tag('ul'):
        for key, value in content.items():
            with tag('li'):
                if type(value) is np.float64:
                    text('{}: {:.6f}'.format(key, value))
                else:
                    text('{}: {}'.format(key, value))

                