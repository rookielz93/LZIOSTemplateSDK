import os, sys
import fileinput

# ======================  edit by yourself  ======================

sources = [
          #'https://github.com/YinTokey/Egen.git',
          ]

project_name = 'LZIOSCommon'
podspec_file_name = 'LZIOSCommon.podspec'

# ==================================================================

new_tag = ""
lib_command = ""
pod_push_command = ""
spec_file_path = "../" + podspec_file_name
find_version_flag = False

def updateVersion():
    print("\n--------- start update version --------\n")
    
    f = open(spec_file_path, 'r+')
    infos = f.readlines()
    f.seek(0, 0)
    file_data = ""
    new_line = ""
    global find_version_flag

    for line in infos:
        if line.find(".version") != -1:
            if find_version_flag == False:
                # find s.version = "xxxx"

                spArr = line.split('.')
                last = spArr[-1]
                last = last.replace('"', '')
                last = last.replace("'", "")
                newNum = int(last) + 1

                arr2 = line.split('"')
                arr3 = line.split("'")

                versionStr = ""
                if len(arr2) > 2:
                    versionStr = arr2[1]

                if len(arr3) > 2:
                    versionStr = arr3[1]
                numArr = versionStr.split(".")

                numArr[-1] = str(newNum)
                # rejoint string
                global new_tag
                for index,subNumStr in enumerate(numArr):
                    new_tag += subNumStr
                    if index < len(numArr)-1:
                        new_tag += "."

                # complete new_tag

                if len(arr2) > 2:
                    line = arr2[0] + '"' + new_tag + '"' + '\n'

                if len(arr3) > 2:
                    line = arr3[0] + "'" + new_tag + "'" + "\n"

                # complete new_line

                print("this is new tag  " + new_tag)
                find_version_flag = True

        file_data += line


    with open(spec_file_path, 'w', ) as f1:
        f1.write(file_data)

    f.close()
    
    print("\n--------- finish update version " + new_tag + " --------\n")

def podCommandEdit():
    print("\n--------- start gen pod command --------\n")
    
    global lib_command
    global pod_push_command
    source_suffix = 'https://github.com/CocoaPods/Specs.git --allow-warnings'
    lib_command = 'pod lib lint --sources='
#    pod_push_command = 'pod repo push ' + project_name + ' ' + podspec_file_name
    pod_push_command = 'pod trunk push ' + podspec_file_name + ' --allow-warnings --use-libraries --verbose'
    if len(sources) > 0:
        # rely on  private sourece
        pod_push_command += ' --sources='

        for index,source in enumerate(sources):
            lib_command += source
            lib_command += ','
            pod_push_command += source
            pod_push_command += ','

        lib_command += source_suffix
        pod_push_command += source_suffix

    else:
        lib_command = 'pod lib lint --allow-warnings --use-libraries --verbose'
    
    print(lib_command + "\n" + pod_push_command)
    print("\n--------- finish gen pod command --------\n")
     
def podLibLint():
    print("\n-------- start exe pod lib lint ---------\n")
    
    oldPath = os.getcwd()
    os.chdir(oldPath+"/../")
    os.system(lib_command)
    os.chdir(oldPath)
    print("\n" + os.getcwd())
    
    print("\n--------- finish exe pod lib lint --------\n")

def gitOperation():
    print("\n--------- start git --------\n")
    
    oldPath = os.getcwd()
    os.chdir(oldPath+"/../")
    
    # git add .
    git_add_command = 'git add .'
    os.system(git_add_command)
    print(git_add_command)
    
    # git commit
    commit_desc = "feat: add tag " + new_tag
    git_commit_command = 'git commit -m "' + commit_desc + '"'
    os.system(git_commit_command)
    print(git_commit_command)
        
    # git push
    r = os.popen('git symbolic-ref --short -q HEAD')
    current_branch = r.read()
    r.close()
    git_push_command = 'git push origin ' + current_branch
    os.system(git_push_command)
    print(git_commit_command)
        
    # git add tag
    git_tag_command = 'git tag -m "' + new_tag + '" ' + new_tag
    os.system(git_tag_command)
    print(git_tag_command)
        
    # git push tags
    git_push_tag_command = 'git push --tags'
    os.system(git_push_tag_command)
    print(git_push_tag_command)
    
    os.chdir(oldPath)
    print("\n--------- finish git --------\n")

def podPush():
    print("\n-------- start pod push ---------\n")
    oldPath = os.getcwd()
    os.chdir(oldPath+"/../")
    
    print(pod_push_command)
    os.system(pod_push_command)
    
    os.chdir(oldPath)
    print("\n-------- finish pod push ---------\n")

# run commands

updateVersion()  # 修改 .podspec 中的 .version
podCommandEdit()
podLibLint()
gitOperation()
podPush()
