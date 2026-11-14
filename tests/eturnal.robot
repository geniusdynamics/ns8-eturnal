*** Settings ***
Library    SSHLibrary

*** Variables ***
${HOST}    eturnal.example.org

*** Test Cases ***
Check if eturnal is installed correctly
    ${output}  ${rc} =    Execute Command    add-module ${IMAGE_URL} 1
    ...    return_rc=True
    Should Be Equal As Integers    ${rc}  0
    &{output} =    Evaluate    ${output}
    Set Suite Variable    ${module_id}    ${output.module_id}

Check if eturnal can be configured
    ${rc} =    Execute Command    api-cli run module/${module_id}/configure-module --data '{"host":"${HOST}","http2https":true,"lets_encrypt":false}'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0

Check if eturnal works as expected
    # eturnal is a STUN/TURN server without a web interface: check that it
    # accepts connections on its TURN port
    ${rc} =    Execute Command    bash -c 'for i in $(seq 1 60); do timeout 3 bash -c "exec 3<>/dev/tcp/127.0.0.1/3478" && exit 0; sleep 5; done; exit 1'
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0

Check if an update repairs subordinate ownership and recovers a stopped service
    ${before} =    Execute Command    runagent -m ${module_id} sh -ec 'sha256sum "$AGENT_STATE_DIR/eturnal.yml"'
    ${rc} =    Execute Command    runagent -m ${module_id} systemctl --user stop eturnal.service
    ...    return_rc=True    return_stdout=False
    Should Be Equal As Integers    ${rc}    0
    ${rc} =    Execute Command    runagent -m ${module_id} sh -ec 'podman unshare chown 9000:9000 "$AGENT_STATE_DIR/eturnal.yml"'
    ...    return_rc=True    return_stdout=False
    Should Be Equal As Integers    ${rc}    0
    ${rc} =    Execute Command    update-module ${IMAGE_URL} ${module_id} --force
    ...    return_rc=True    return_stdout=False
    Should Be Equal As Integers    ${rc}    0
    ${after} =    Execute Command    runagent -m ${module_id} sh -ec 'sha256sum "$AGENT_STATE_DIR/eturnal.yml"'
    Should Be Equal    ${before}    ${after}
    ${rc} =    Execute Command    runagent -m ${module_id} sh -ec 'test "$(stat -c %u "$AGENT_STATE_DIR/eturnal.yml")" = "$(id -u)" && systemctl --user is-active eturnal.service && systemctl --user is-active eturnal-app.service'
    ...    return_rc=True    return_stdout=False
    Should Be Equal As Integers    ${rc}    0

Check if eturnal is removed correctly
    ${rc} =    Execute Command    remove-module --no-preserve ${module_id}
    ...    return_rc=True  return_stdout=False
    Should Be Equal As Integers    ${rc}  0
