def conv_kb_to_mb(input_kilobyte):
        megabyte = 1./1000
        convert_mb = megabyte * input_kilobyte
        return convert_mb


def conv_mb_to_gb(input_megabyte):
    gigabyte = 1.0/1024
    convert_gb = gigabyte * input_megabyte
    return convert_gb