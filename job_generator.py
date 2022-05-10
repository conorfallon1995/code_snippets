import os

# Edit these as needed
registry_name = "registry_name"
image_name = "image_name"
script_name = "script_name"

# Where the XML files are located, no '/' needed
xml_directory = "xmls"

# Make a directory first to prevent 1000 yml files going somewhere they're not wanted...
# Need to add a '/' at the end of directory name
write_directory = ""

# Creates list of names of all xml files in xml_directory directory
files = [f for f in os.listdir(xml_directory) if os.path.isfile(os.path.join(xml_directory, f)) and f.endswith('.xml')]

for name in files:
    with open(write_directory + str(os.path.splitext(name)[0]) + '.yml', 'w') as f:
        yaml_str = f"""\
apiVersion: batch/v1
kind: Job
    metadata:
    name: run-soup-{os.path.splitext(name)[0]}
    labels:
        app: run-soup-{os.path.splitext(name)[0]}
    spec:
    template:
        metadata:
        labels:
            app: run-soup-{os.path.splitext(name)[0]}
        spec:
        containers:
            - name: {registry_name}
            image: {image_name}
            command: [
                "python", "{script_name}",]
            args: [
                "{name}",
                "{os.path.splitext(name)[0]}_clean.txt"]
            volumeMounts:
            - mountPath: "/pvc/output/soup"
                name: pvc-output-soup
            resources:
                limits:
                cpu: 1
        memory: 1Gi
        nodeSelector:
            gpu: p100
        volumes:
            - name: pvc-output
            persistentVolumeClaim:
                claimName: pvc
        imagePullSecrets:
        - name: private-registry-auth
        restartPolicy: Never

    """.format()
        f.write(yaml_str)
