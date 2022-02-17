import subprocess

def run(pdffile):

    cmd = ["pdftotext", pdffile, "/dev/stdout"]

    output = None
    with subprocess.Popen(cmd, stdout=subprocess.PIPE) as ps:
        output = ps.communicate()[0]
        if ps.returncode != 0:
            # should raise
            exit(1)

    return output
