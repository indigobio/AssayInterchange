var app = angular.module('fileUpload', ['ngFileUpload', 'ngFileSaver']);

app.controller('MyCtrl', ['FileSaver', 'Blob', '$http', '$scope', 'Upload', '$timeout', function (FileSaver, Blob, $http, $scope, Upload, $timeout) {

    var self = this;
    var file = null;

    $scope.filedata = {
        assay: '',
        format: '',
        message: '',
        valid: false
    };

    $scope.$watch('files', function () {
        $scope.upload($scope.files);
    });
    $scope.$watch('file', function () {
        if ($scope.file != null) {
            $scope.files = [$scope.file];
        }
    });
    $scope.log = '';

    $scope.upload = function (files) {
        if (files && files.length) {
            for (var i = 0; i < files.length; i++) {
                var file = files[i];
                self.file = file;
                if (!file.$error) {
                    Upload.upload({
                        url: '/validate',
                        data: {
                            file: file
                        }
                    }).then(function (resp) {
                        $timeout(function() {
                            $scope.log = 'file: ' +
                                resp.config.data.file.name +
                                '\n' + $scope.log;
                            $scope.filedata = resp.data;
                            console.log(self.file);
                            Upload.upload({
                                url: '/',
                                data: {
                                    file: self.file
                                }
                            }).then(function (resp) {
                                var dl;
                                if (resp.headers()['content-type'] === 'application/json') {
                                    dl = new Blob([JSON.stringify(resp.data, null, 4)], {type: resp.headers()['content-type'] + ";charset=utf-8"})
                                } else if (resp.headers()['content-type'] === 'application/vnd.ms-excel') {
                                    var bytechars = atob(resp.data);
                                    var bytenums = new Array(bytechars.length);
                                    for (var i=0; i < bytechars.length; i++) {
                                        bytenums[i] = bytechars.charCodeAt(i);
                                    }
                                    var bytearray = new Uint8Array(bytenums);
                                    dl = new Blob([bytearray], {type: "application/octet-stream"})
                                }
                                FileSaver.saveAs(dl, resp.headers()['filename']);
                            });
                        });
                    }, null, function (evt) {
                        var progressPercentage = parseInt(100.0 *
                            evt.loaded / evt.total);
                        $scope.log = 'progress: ' + progressPercentage +
                            '% ' + evt.config.data.file.name + '\n' +
                            $scope.log;
                    });
                }
            }
        }
    };
}]);