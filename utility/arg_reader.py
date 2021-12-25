# Read the arguments given and pass them back in the format the main function uses them
def read_args(args: list):
    f_in = ''
    f_out = ''

    for arg in args:
        idx = args.index(arg)
        
        if args[idx] == '-i' or args[idx] == '-in':
            if len(args) <= idx + 1:
                raise ValueError('No input file specified')
            f_in = args[idx + 1].strip()

        if args[idx] == '-o' or args[idx] == '-out':
            if len(args) <= idx + 1:
                raise ValueError('No output file specified')
            f_out = args[idx + 1].strip()




    return (f_in, f_out)