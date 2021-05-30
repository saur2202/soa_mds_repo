#!groovy
pipeline {
    agent any
    
    parameters {
        booleanParam(name: 'P_UNDEPLOY', defaultValue: params.UNDEPLOY_MDS ?: false, description: 'UnDeploy MDS')
    }

    environment {
        SOA_CREDENTIALS = credentials('DEV_SOA_DEPLOYER')
        UNDEPLOY = "${params.P_UNDEPLOY ?: false}"
    }

    stages {

        stage('Source') { 
            steps { //Get source code from Git  
                checkout scm
            }
        }

        stage('Compile') {
            when {
                beforeAgent true
                anyOf {
                    expression { params.P_UNDEPLOY == false }
                }
            }
            steps { //Create jar file
                echo 'LOG: Zipping the mds artifacts into the jar format'
                sh """cd apps
                zip -r ../mds_${env.BUILD_ID}.jar ."""
            }
        }

        stage('UnDeploy') {
            when {
                beforeAgent true
                anyOf {
                    expression { params.P_UNDEPLOY == true }
                }
            }
            steps { 
                // Load environment variables
                echo 'INFO: Loading environment variables'
                load "${env.BRANCH_NAME}.env"

                // UnDeploy mds 
                echo 'INFO: Running wlst to undeploy MDS'
                sh """#!/bin/bash
                ${env.WLST_HOME}/wlst.sh undeployMDS.py"""

            }
        }

        stage('Deploy') {
            when {
                beforeAgent true
                anyOf {
                    expression { params.P_UNDEPLOY == false }
                }
            }
            steps { 
                // Load environment variables
                echo 'INFO: Loading environment variables'
                load "${env.BRANCH_NAME}.env"

                // Deploy mds jar
                echo 'INFO: Running wlst to deploy MDS jar'
                sh """#!/bin/bash
				sh sudo su oracle
                ${env.WLST_HOME}/wlst.sh deployMDS.py -fromLocation mds_${env.BUILD_ID}.jar"""
            }
        }	
		
    }
	
	post {
			always {
				emailext attachLog:true, body: 'Check console output at $BUILD_URL to view the results of MDS deployment',
                to: 'saurabhleeds@gmail.com',
                subject: 'MDS Deployment Status : $PROJECT_NAME - #$BUILD_NUMBER',
                from: 'jenkins.test@test.com'
        }
    }
}
