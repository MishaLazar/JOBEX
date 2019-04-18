import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { LoadingController } from '@ionic/angular';
import { StorageService } from 'src/app/services/storage.service';
import { Token } from 'src/app/models/token.model';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  loginForm:FormGroup;
  constructor(public formBuilder: FormBuilder,private storageSVC:StorageService,private authSvc:AuthenticationService,public loadingController: LoadingController) {
    this.buildForm();
   }

  ngOnInit() {
  }
  buildForm(){
    this.loginForm = this.formBuilder.group({
      mail:['',Validators.compose([Validators.required,Validators.email])],
      password:['',Validators.compose([Validators.required,Validators.minLength(4)])]
    });
  }
  async onLogin(){
    if (!this.loginForm.valid) {
      return;
    }
    const userName = this.loginForm.get('mail').value;
    const userPassword = this.loginForm.get('password').value;
    const loading = await this.loadingController.create({
      message:'login in ...'
    });
    loading.present();
    this.authSvc.onSignin(userName,userPassword).subscribe(
      () => {
      (response:Token) => {
        this.storageSVC.setStorageValueByKey('access_token',response.access_token);
        this.storageSVC.setStorageValueByKey('refresh_token',response.refresh_token);
        loading.dismiss();
      }
    })
  
}

async presentLoading() {
  const loading = await this.loadingController.create({
    message: 'Hellooo',
    duration: 2000
  });
  await loading.present();
}

}
