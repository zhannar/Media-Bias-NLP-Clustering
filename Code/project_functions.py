def summerize_pickles(notebook_path):
    from IPython.nbformat import current as nbformat
    import re

    with open(notebook_path) as fh:
        nb = nbformat.reads_json(fh.read())
        
    list_of_input_pickles = []
    list_of_output_pickles = []

    for cell in nb["worksheets"][0]["cells"]:
        # This confirms there is at least one pickle in it.
        if cell["cell_type"] != "code" or cell["input"].find("pickle") == -1:   # Skipping over those cells which aren't code or those cells with code but which don't reference "pickle
            continue

        cell_content = cell["input"]

        # In case there are multiple lines, it iterates line by line.
        for line in cell_content.splitlines():
            if line.find("pickle") == -1:  # Skips over lines w/ no mention of "pickle" to potentially reduce the number of times it's searched.
                continue
            ############################    ############################    ############################    ############################
            code_type = str()
            if line.find("pickle.dump") != -1 or line.find(".to_pickle")!= -1:
                code_type = "output"       
            elif line.find("pickle.load") != -1 or line.find(".read_pickle")!= -1:
                code_type = "input"
            else:
                continue   # This tells the code to skip over lines like "import cpickle as pickle"
            ############################    ############################    ############################    ############################
            filename = re.findall(r'"(.*?)"', line)   # This gets all the content between the quotes. See: http://stackoverflow.com/questions/171480/regex-grabbing-values-between-quotation-marks    
            ############################    ############################    ############################    ############################        
            if code_type == "input":
                list_of_input_pickles.append(filename[0])
            elif code_type == "output":
                list_of_output_pickles.append(filename[0])

    pickles_dict = {"input_pickles":list_of_input_pickles,
                    "output_pickles":list_of_output_pickles }
    
    return pickles_dict
