import {Injectable} from "@angular/core";

@Injectable()
export class ConfigService {

  private api_url = 'http://127.0.0.1:5050/';


  getApiUrl(){
    return this.api_url;
  }

}
