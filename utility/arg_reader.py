args_known = ['-i', '-in', '-o', '-out', '-w', '-width', '-h', '-height']

# Read the arguments given and pass them back in the format the main function uses them
def read_args(args: list):
    f_in = ''
    f_out = ''
    w = None
    h = None

    for arg in args:
        idx = args.index(arg)
        
        if args[idx] == '-i' or args[idx] == '-in':
            check_arg('input name', args, idx, 1)
            f_in = args[idx + 1].strip()

        if args[idx] == '-o' or args[idx] == '-out':
            check_arg('output file', args, idx, 1)
            f_out = args[idx + 1].strip()

        if args[idx] == '-w' or args[idx] == '-width':
            check_arg('output width', args, idx, 1)
            try:
                w = int(args[idx + 1].strip())
            except:
                raise ValueError('Target output width should be an integer')
        
        if args[idx] == '-h' or args[idx] == '-height':
            check_arg('output height', args, idx, 1)
            try:
                h = int(args[idx + 1].strip())
            except:
                raise ValueError('Target output height should be an integer')
        
    return (f_in, f_out, (w, h))

def check_arg(argument: str, args: list, idx: int, values: int):
    if len(args) <= idx + values:
        raise ValueError(f'No {argument} specified')
    if args[idx + 1] in args_known:
        raise ValueError(f'No {argument} specified')