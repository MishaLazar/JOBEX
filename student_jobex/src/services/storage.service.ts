import {Injectable} from "@angular/core";
// import {Storage} from "@ionic/storage";

@Injectable()
export class StorageService {
  constructor (){}


  setStorageValueByKey(key:string,val:any){
    localStorage.setItem(key,val);
  }
    /*this.storage.set(key,val)
      .then(value =>
        console.log(value)
      )
      .catch(reason =>{
          console.log(reason.toString())
        }
      );

  }*/

  getValueByKey(key:string){
    return localStorage.getItem(key);
    /*this.storage.get(key)
      .then(
        value =>{
          return value;
        }
      )
      .catch(
        reason => {
          console.log("Oops and Error: " + reason.toString())
        }
      )
*/
  }

  removeItemByKey(key:string) {

    localStorage.removeItem(key);
    /*this.storage.remove(key)
      .then(value =>
        console.log('removed :' + value )
      );

  }*/
  }
}

