pipeline {
        agent any

        stages {
            stage('下载文件') {
                parallel {
                    stage('内核源') {
                        steps {
                            dir('SOURCES') {
                                sh 'wget -c http://mirrors.163.com/kernel/v5.x/linux-5.12.10.tar.gz'
                            }
                        }
                    }
                    stage('调度补丁') {
                        steps {
                            dir('SOURCES') {
                                sh 'wget -c http://ck.kolivas.org/patches/muqss/5.0/5.12/0001-MultiQueue-Skiplist-Scheduler-v0.210.patch'
                            }
                        }
                    }
                }
            }

            stage('构建内核包') {
                steps {
                    sh 'rpmbuild --define "_topdir $(pwd)" -bb kernel.spec'
                }
            }
        }
    // Post trigger
    post {
        always {
            emailext body: '''
<!DOCTYPE html>
<html>

    <body leftmargin="8" marginwidth="0" topmargin="8" marginheight="4" offset="0">
        <table width="95%" cellpadding="0" cellspacing="0"  style="font-size: 11pt; font-family: Tahoma, Arial, Helvetica, sans-serif">
        <tr>
            <br>
                This email was sent by Jenkins
            </br>
        </tr>
        <tr>
            <td>
                <b>
                    <br>
                        <font color="#6E6E6E">Project details</font>
                    </br>
                </b>
                <hr size="2" width="100%" align="center" />
            </td>
        </tr>
        <tr>
            <td>
                <ul>
                    <li>Project name: ${PROJECT_NAME}</li>
                    <li>Build branch: ${BRANCH_NAME}</li>
                    <li>Build number: #${BUILD_NUMBER}</li>
                    <li>Build result: ${BUILD_STATUS}</li>
                    <li>Trigger: ${CAUSE}</li>
                </ul>
                <hr size="2" width="100%" align="center" />
            </td>
        </tr>
        <tr>
            <td>
                <b>
                    <br>
                        <font color="#6E6E6E">Console output: <a href="${BUILD_URL}console">${PROJECT_NAME} #${BUILD_NUMBER}</a></font>
                    </br>
                </b>
            </td>
        </tr>
        </table>
    </body>
</html>
            ''',
            subject: 'Jenkins - $PROJECT_NAME build was $BUILD_STATUS #$BUILD_NUMBER',
            to: '${DEFAULT_RECIPIENTS}'
        }

        success {
            dir('RPMS') {
                archiveArtifacts artifacts: '*/*.rpm',
                fingerprint: true,
                onlyIfSuccessful: true
            }
        }

        cleanup {
            cleanWs deleteDirs: true
        }
    }
}
