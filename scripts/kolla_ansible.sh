#!/bin/bash
## --- STEP0 ---
installer_dir="$(pwd)"
current_step="STEP0"
if [ -f $installer_dir/current_step.tmp ]; then
    echo "Instalasi sebelumnya mungkin terhenti, lanjukan?"
    echo "(Y untuk Ya, ENTER untuk mulai ulang)"
    read continue
fi
if [[ -n "$continue" ]]; then
    input="$installer_dir/current_step.tmp"
    while IFS= read -r loaded_step
    do
      echo "LOADING $loaded_step ..."
      current_step=loaded_step
    done < "$input"
fi

## --- STEP1 ---
if [[ $continue != "Y" ]] || [[ $continue != "y" ]] && [[ $current_step == "STEP0" ]]; then
    echo "===STEP====="
    echo "====KOLLA ANSIBLE====="
    kolla-genpwd
    if [ $? -eq 0 ]; then
        echo 'OK'
        kolla-ansible certificates
        if [ $? -eq 0 ]; then
            echo "Certificate SUCCESSS"
            kolla-ansible bootstrap-servers

            if [ $? -eq 0 ]; then
                echo "BOOTSTRAP SUCCESS"
                kolla-ansible prechecks

                if [ $? -eq 0 ]; then
                    kolla-ansible deploy
                    echo "RUN COMMAND SUCCESSFULL"
                else
                    echo "ERROR DEPLOY"
                fi
            else
                echo "BOOTSTRAP ERROR"
            fi
        else
            echo "Certificate FAILED"
        fi
    else
        echo "FAILED RUN KOLLA"
    fi
fi
