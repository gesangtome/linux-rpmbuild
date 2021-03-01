pipeline {
        agent any

        stages {
            stage('Allocate space') {
                parallel {
                    stage('rpmbuild') {
                        steps {
                            sh 'mkdir -p {BUILD,BUILDROOT,RPMS,SOURCES,SRPMS}'
                        }
                    }
                    stage('patch') {
                        steps {
                            sh 'mkdir -p patches'
                        }
                    }
                }
            }

            stage('Download files') {
                parallel {
                    stage('download linux release') {
                        steps {
                            sh 'wget -P SOURCES https://mirrors.tuna.tsinghua.edu.cn/kernel/v5.x/linux-5.11.tar.xz'
                        }
                    }
                    stage('download ck-1 patches') {
                        steps {
                            sh 'wget -P patches -i http://ck.kolivas.org/patches/5.0/5.11/5.11-ck1/patches/series'
                        }
                    }
                }
            }

            stage('Unzip archive') {
                steps {
                    dir('SOURCES') {
                        sh 'xz -dc linux-5.11.tar.xz| tar -xvf -'
                    }
                }
            }

            stage('Apply patches') {
                parallel {
                    stage('Apply kernel ck-1 patches') {
                        steps {
                            dir('SOURCES/linux-5.11') {
                                sh 'for file in ../../patches/*.patch; do patch -p1 $file; done'
                            }
                        }
                    }
                    stage('Apply misc patches') {
                        steps {
                            dir('SOURCES/linux-5.11') {
                                sh 'for file in ../../misc/*.patch; do patch -p1 $file; done'
                            }
                        }
                    }
                }
            }

            stage('Generate defconfig') {
                steps {
                    dir('SOURCES/linux-5.11') {
                        sh 'yes "" | make oldconfig'
                    }
                }
            }

            stage('Generate source') {
                steps {
                    dir('SOURCES') {
                        sh '''
                            mv linux-5.11 kernel-5.11.0 || false
                        '''
                    }
                }
            }

            stage('Generate links') {
                parallel {
                    stage('for kernel-devel') {
                        steps {
                            dir('SOURCES') {
                                sh 'ln -sf kernel-5.11.0 kernel-devel-5.11.0 || false'
                            }
                        }
                    }
                    stage('for kernel-headers') {
                        steps {
                            dir('SOURCES') {
                                sh 'ln -sf kernel-5.11.0 kernel-headers-5.11.0 || false'
                            }
                        }
                    }
                    stage('for kernel-modules') {
                        steps {
                            dir('SOURCES') {
                                sh 'ln -sf kernel-5.11.0 kernel-modules-5.11.0 || false'
                            }
                        }
                    }
                }
            }

            stage('Generate rpm sources') {
                parallel {
                    stage('for kernel') {
                        steps {
                            dir('SOURCES') {
                                sh 'tar -zcvhf kernel-5.11.0.tar.gz kernel-5.11.0 || false'
                            }
                        }
                    }
                    stage('for kernel-devel') {
                        steps {
                            dir('SOURCES') {
                                sh 'tar -zcvhf kernel-devel-5.11.0.tar.gz kernel-devel-5.11.0 || false'
                            }
                        }
                    }
                    stage('for kernel-headers') {
                        steps {
                            dir('SOURCES') {
                                sh 'tar -zcvhf kernel-headers-5.11.0.tar.gz kernel-headers-5.11.0 || false'
                            }
                        }
                    }
                    stage('for kernel-modules') {
                        steps {
                            dir('SOURCES') {
                                sh 'tar -zcvhf kernel-modules-5.11.0.tar.gz kernel-modules-5.11.0 || false'
                            }
                        }
                    }
                }
            }

            stage('Build rpm packages') {
                parallel {
                    stage('building kernel') {
                        steps {
                            sh 'rpmbuild --define "_topdir $(pwd)" -bb kernel.spec'
                        }
                    }
                    stage('building kernel-devel') {
                        steps {
                            sh 'rpmbuild --define "_topdir $(pwd)" -bb kernel-devel.spec'
                        }
                    }
                    stage('building kernel-headers') {
                        steps {
                            sh 'rpmbuild --define "_topdir $(pwd)" -bb kernel-headers.spec'
                        }
                    }
                    stage('building kernel-modules') {
                        steps {
                            sh 'rpmbuild --define "_topdir $(pwd)" -bb kernel-modules.spec'
                        }
                    }
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
                archiveArtifacts artifacts: 'aarch64/kernel-*.rpm',
                fingerprint: true,
                onlyIfSuccessful: true
            }
        }

        cleanup {
            cleanWs deleteDirs: true
        }
    }
}
