import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';
import { AuthenticationService } from 'src/app/services/authentication.service';
import { LoadingController, ToastController } from '@ionic/angular';
import { StorageService } from 'src/app/services/storage.service';
import { Token } from 'src/app/models/token.model';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { Router } from '@angular/router';
import { error } from 'util';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  loginForm:FormGroup;
  constructor(
    public formBuilder: FormBuilder,
    private storageSVC:StorageService,
    private auth:AuthenticationService,
    public loadingController: LoadingController,
    private profile:MyProfileService, private router:Router,public toastController: ToastController) {
   
   }

  ngOnInit() {
    this.buildForm();
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
    this.auth.onSignin(userName,userPassword).subscribe(
      
      (response:any) => {
        let user_id = response['user_id'];
        let access_token = response['access_token'];
        let refresh_token = response['refresh_token'];
        
        this.profile.setUserIdOnLogin(user_id); 
        this.storageSVC.setStorageValueByKey('user_id',user_id);
        this.storageSVC.setStorageValueByKey('access_token',access_token);
        this.storageSVC.setStorageValueByKey('refresh_token',refresh_token);
        loading.dismiss();        
        this.auth.stateSubject.next('login');
        this.router.navigateByUrl('/')
    },
    error => {
      loading.dismiss();
      this.incorrectLogin();
      
    }
    );
  
}
 async incorrectLogin() {
    const toast  = await this.toastController.create({
      message: 'email or password is incorrect',
      position:"bottom",
      duration: 2000
    });
    toast.present();
  }




onRegister(){
  this.router.navigateByUrl('/register');
}
}
