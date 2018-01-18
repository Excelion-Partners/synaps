var app = angular.module('interfaceApp', []);

app.controller('interfaceController', function($scope, $http) {

    $scope.pageObject = {"wifiMaster": false, "ethernetInterfaces": [], "wirelessInterfaces": []};

    $scope.getInterfaceDevices = function() {
      $http.get('/getinterfaces')
      .then(function(result) {
          $scope.addObjectProperties(result.data);
      });
    };

    $scope.saveButtonEnabled = true;

    $scope.addObjectProperties = function(data){
      for(var i = 0; i < data.length; i++){
        if(data[i].InterfaceTypeId == "1"){
          //ethernet
          $scope.pageObject.ethernetInterfaces.push({
                    "enabled": false,
                    "dhcp": true,
                    "ifaceType": "Ethernet",
                    "ifaceName": data[i].InterfaceName,
                    "ifacePath": data[i].InterfacePath,
                    "staticIp": "",
                    "staticNetmask": "",
                    "staticGateway": ""});
        } else {
          //wifi
          $scope.pageObject.wirelessInterfaces.push({
                    "enabled": false,
                    "dhcp": true,
                    "ifaceType": "Wireless",
                    "ifaceName": data[i].InterfaceName,
                    "ifacePath": data[i].InterfacePath,
                    "ssid": "",
                    "passphrase": "",
                    "staticIp": "",
                    "staticNetmask": "",
                    "staticGateway": ""})
        }
      }
    };

    $scope.saveInterfaces = function(){

      $scope.saveButtonEnabled = false;

      var formBody = [];
      var encodedKey = encodeURIComponent('data');
      var encodedValue = encodeURIComponent(JSON.stringify($scope.pageObject));
      formBody.push(encodedKey + "=" + encodedValue);
      formBody = formBody.join("&");

      var req = {
        method: 'POST',
        url: '/saveinterfaces',
        headers: {
         'Content-Type': 'application/x-www-form-urlencoded'
        },
        data: formBody
      }

      $http(req).then(function(msg){
        console.log(msg.data);

        alert(msg.data);
      }, function(){});
    };

    $scope.getInterfaceDevices();
});
