#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2021 LG Electronics Inc.
# SPDX-License-Identifier: Apache-2.0
import os
from fosslight_util.write_excel import write_result_to_excel, write_result_to_csv
from fosslight_util.write_opossum import write_opossum
from fosslight_util.write_yaml import write_yaml

SUPPORT_FORMAT = {'excel': '.xlsx', 'csv': '.csv', 'opossum': '.json', 'yaml': '.yaml'}


def check_output_format(output='', format='', customized_format={}):
    success = True
    msg = ''
    output_path = ''
    output_file = ''
    output_extension = ''

    if customized_format:
        support_format = customized_format
    else:
        support_format = SUPPORT_FORMAT

    if format:
        format = format.lower()
        if format not in list(support_format.keys()):
            success = False
            msg = 'Enter the supported format with -f option: ' + ', '.join(list(support_format.keys()))
        else:
            output_extension = support_format[format]

    if success:
        if output != '':
            basename_extension = ''
            if not os.path.isdir(output):
                output_path = os.path.dirname(output)

                basename = os.path.basename(output)
                basename_file, basename_extension = os.path.splitext(basename)
            if basename_extension:
                if format:
                    if output_extension != basename_extension:
                        success = False
                        msg = f"Enter the same extension of output file(-o:'{output}') with format(-f:'{format}')."
                else:
                    if basename_extension not in support_format.values():
                        success = False
                        msg = 'Enter the supported file extension: ' + ', '.join(list(support_format.values()))
                if success:
                    output_file = basename_file
                    output_extension = basename_extension
            else:
                output_path = output

    return success, msg, output_path, output_file, output_extension


def check_output_formats(outputs=[], formats=[], customized_format={}):
    success = True
    msg = ''
    output_paths = []
    output_files = []
    output_extensions = []

    if customized_format:
        support_format = customized_format
    else:
        support_format = SUPPORT_FORMAT

    if formats:
        # If -f option exist
        formats = [format.lower() for format in formats]
        for format in formats:
            if format not in list(support_format.keys()):
                success = False
                msg = 'Enter the supported format with -f option: ' + ', '.join(list(support_format.keys()))
            else:
                output_extensions.append(support_format[format])

    if success:
        if len(outputs) == 1 and not os.path.splitext(outputs[0])[1]:
            # Case 1: Single directory
            output_paths.append(outputs[0])
        elif len(outputs) == 1 and os.path.splitext(outputs[0])[1] and len(formats) == 0:
            # Case 2 : Single file without -f option
            output_paths.append(os.path.dirname(outputs[0]))

            basename = os.path.basename(outputs[0])
            basename_file, basename_extension = os.path.splitext(basename)
            if basename_extension not in support_format.values():
                success = False
                msg = 'Enter the supported file extension: ' + ', '.join(list(support_format.values()))
            else:
                output_files.append(basename_file)
                output_extensions.append(basename_extension)
        else:
            # Case 3: Multiple files
            if len(outputs) != len(formats) and len(outputs) != 0:
                # The number of -o and -f options must match when specifying file names.
                success = False
                msg = "The number of -o and -f options must match when specifying file names."
                return success, msg, output_paths, output_files, output_extensions

            for output, format in zip(outputs, formats):
                output_path = os.path.dirname(output)
                basename = os.path.basename(output)
                basename_file, basename_extension = os.path.splitext(basename)

                if not basename_extension or basename_extension != support_format[format]:
                    # Output file extension does not match the specified format.
                    success = False
                    msg = f"Output file '{output}' does not match the specified format '{format}'."
                    return success, msg, output_paths, output_files, output_extensions

                output_paths.append(output_path)
                output_files.append(basename_file)
    if not output_paths:
        output_paths.append('')
    if not output_files:
        output_files.append('')
    return success, msg, output_paths, output_files, output_extensions


def write_output_file(output_file_without_ext, file_extension, sheet_list, extended_header={}, hide_header={}, cover=""):
    success = True
    msg = ''

    if file_extension == '':
        file_extension = '.xlsx'
    result_file = output_file_without_ext + file_extension

    if file_extension == '.xlsx':
        success, msg = write_result_to_excel(result_file, sheet_list, extended_header, hide_header, cover)
    elif file_extension == '.csv':
        success, msg, result_file = write_result_to_csv(result_file, sheet_list)
    elif file_extension == '.json':
        success, msg = write_opossum(result_file, sheet_list)
    elif file_extension == '.yaml':
        success, msg, result_file = write_yaml(result_file, sheet_list, False)
    else:
        success = False
        msg = f'Not supported file extension({file_extension})'

    return success, msg, result_file


def write_output_files(combined_paths_and_files, file_extensions, sheet_list, extended_header={}, hide_header={}, cover=""):
    results = []
    for output_file_without_ext, file_extension in zip(combined_paths_and_files, file_extensions):
        success = True
        msg = ''

        if file_extension == '':
            file_extension = '.xlsx'
        result_file = output_file_without_ext + file_extension

        if file_extension == '.xlsx':
            success, msg = write_result_to_excel(result_file, sheet_list, extended_header, hide_header, cover)
        elif file_extension == '.csv':
            success, msg, result_file = write_result_to_csv(result_file, sheet_list)
        elif file_extension == '.json':
            success, msg = write_opossum(result_file, sheet_list)
        elif file_extension == '.yaml':
            success, msg, result_file = write_yaml(result_file, sheet_list, False)
        else:
            success = False
            msg = f'Not supported file extension({file_extension})'

        results.append((success, msg, result_file))
    return results
