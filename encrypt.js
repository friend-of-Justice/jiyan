var name = "The Window";

var object = {
　　　　name : "My Object",

　　　　getNameFunc : function(){
          console.log("111",this)
　　　　　　return function(){
              console.log("222",this)
　　　　　　　　return this.name;
　　　　　　};

　　　　}

};

console.log(object.getNameFunc()());