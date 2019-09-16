module.exports = function(grunt) {
    
    var cssCustomTempFile = 'django_nanosourcer/static/src/css/custom/.custom.css';
    var cssVendorTempFile = 'django_nanosourcer/static/src/css/vendor/.vendor.css';
    var jsCustomTempFile = 'django_nanosourcer/static/src/js/custom/.custom.js';
    var jsVendorTempFile = 'django_nanosourcer/static/src/js/vendor/.vendor.js';

    var cssCustom = [];

    var cssVendor = [

        'django_nanosourcer/static/src/fonts/glyphicon.css',
        'django_nanosourcer/static/src/fonts/open-sans.css',
        'django_nanosourcer/static/src/css/vendor/flickity.2.0.3.css',
        'django_nanosourcer/static/src/css/vendor/leaflet-0.7.7.css',
        'django_nanosourcer/static/src/css/vendor/leaflet-areaselect.css',
        'django_nanosourcer/static/src/css/vendor/leaflet-locationfilter.css',
        'django_nanosourcer/static/src/css/vendor/leaflet-control-window.css',
        'django_nanosourcer/static/src/css/vendor/viewer.css',
        'django_nanosourcer/static/src/css/vendor/bootstrap.css'

    ];

    var jsCustom = [

        'django_nanosourcer/static/src/js/custom/Container.js',
        'django_nanosourcer/static/src/js/custom/Card.js',
        'django_nanosourcer/static/src/js/custom/Navbar.js',
        'django_nanosourcer/static/src/js/custom/MetadataItem.js',
        'django_nanosourcer/static/src/js/custom/StatusCardBody.js',
        'django_nanosourcer/static/src/js/custom/MapWidget.js',
        'django_nanosourcer/static/src/js/custom/GLSRequestPreparer.js',
        'django_nanosourcer/static/src/js/custom/PeriodWidget.js',
        'django_nanosourcer/static/src/js/custom/main.js'

    ];

    var jsTest = [

        'django_nanosourcer/static/js/vendor/qunit-2.0.1.js'

    ];

    var jsVendor = [

        'django_nanosourcer/static/src/js/vendor/jquery-3.1.0.js',
        'django_nanosourcer/static/src/js/vendor/jquery-ui.min.js',
        'django_nanosourcer/static/src/js/vendor/flickity.min.2.0.3.js',
        'django_nanosourcer/static/src/js/vendor/viewer.min.js',
        'django_nanosourcer/static/src/js/vendor/leaflet-0.7.7.js',
        'django_nanosourcer/static/src/js/vendor/leaflet.locationfilter.js',
        'django_nanosourcer/static/src/js/vendor/leaflet-areaselect.js',
        'django_nanosourcer/static/src/js/vendor/leaflet-control-window.js',
        'django_nanosourcer/static/src/js/vendor/spin.min.js',
        'django_nanosourcer/static/src/js/vendor/apiGateway-js-sdk/lib/axios/dist/axios.standalone.js',
        'django_nanosourcer/static/src/js/vendor/apiGateway-js-sdk/lib/CryptoJS/rollups/hmac-sha256.js',
        'django_nanosourcer/static/src/js/vendor/apiGateway-js-sdk/lib/CryptoJS/components/hmac.js',
        'django_nanosourcer/static/src/js/vendor/apiGateway-js-sdk/lib/CryptoJS/components/enc-base64.js',
        'django_nanosourcer/static/src/js/vendor/apiGateway-js-sdk/lib/url-template/url-template.js',
        'django_nanosourcer/static/src/js/vendor/apiGateway-js-sdk/lib/apiGatewayCore/sigV4Client.js',
        'django_nanosourcer/static/src/js/vendor/apiGateway-js-sdk/lib/apiGatewayCore/apiGatewayClient.js',
        'django_nanosourcer/static/src/js/vendor/apiGateway-js-sdk/lib/apiGatewayCore/simpleHttpClient.js',
        'django_nanosourcer/static/src/js/vendor/apiGateway-js-sdk/lib/apiGatewayCore/utils.js',
        'django_nanosourcer/static/src/js/vendor/apiGateway-js-sdk/apigClient.js'

    ];

    var scssCustom = [

        'django_nanosourcer/static/src/css/nanosourcer.scss'

    ];

    var scssVendor = [];


    grunt.initConfig({
      
        pkg: grunt.file.readJSON('package.json'),
        uglify: {
            all: {
                options: {
                    mangle: false
                },
                files: {
                    'django_nanosourcer/static/dist/nanosourcer.min.js': [jsVendor, jsCustom]
                }
            },
            test: {
                options: {
                    mangle: false
                },
                files: {
                    'django_nanosourcer/static/test/nanosourcer.min.js': [jsVendor, jsTest, jsCustom]
                }
            },
            custom: {
                options: {
                    mangle: false
                },
                files: {
                    'django_nanosourcer/static/src/js/custom/.custom.js': jsCustom
                }
            },
            vendor: {
                options: {
                    mangle: false
                },
                files: {
                    'django_nanosourcer/static/src/js/vendor/.vendor.js': jsVendor
                }
            },
            temp: {
                options: {
                    mangle: false
                },
                files: {
                    'django_nanosourcer/static/dist/nanosourcer.min.js': [jsVendorTempFile, jsCustomTempFile]
                }
            }

        },
        sass: {
            options: {},
            custom: {
                files: {
                    'django_nanosourcer/static/src/css/custom/.custom.css': [scssCustom]
                }
            }
        },
        concat: {
            all: {
                files: {
                    'django_nanosourcer/static/dist/nanosourcer.css': [cssCustomTempFile, cssVendorTempFile]
                }
            },
            vendor: {
                files: {
                    'django_nanosourcer/static/src/css/vendor/.vendor.css': [cssVendor]
                }
            }
        },
        clean: {
            'css-custom': [cssCustomTempFile],
            'css-vendor': [cssVendorTempFile],
            'js-custom': [jsCustomTempFile],
            'js-vendor': [jsVendorTempFile]
        }

    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-reload');

    grunt.registerTask('default', ['uglify', 'sass', 'concat', 'clean']);

};