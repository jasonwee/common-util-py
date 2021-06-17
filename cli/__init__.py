import subprocess

def run(command):
    #bashCommand = "cwm --rdf test.rdf --ntriples > test.nt"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return (output, error)
