import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MyProfileService } from 'src/app/services/my-profile.service';
import { LoadingController } from '@ionic/angular';
import { StorageService } from 'src/app/services/storage.service';
import { Token } from 'src/app/models/token.model';
import { Registration } from 'src/app/models/registration';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage implements OnInit {
  

  registerForm:FormGroup;
  constructor(
    public formBuilder: FormBuilder,
    private myProfile:MyProfileService,
    private loadingController:LoadingController,
    private router:Router,
    private storageSVC:StorageService) { 


    this.buildForm();
  }

  ngOnInit() {

  }

  buildForm(): any {
    this.registerForm = this.formBuilder.group({
      firstName:['',Validators.compose([Validators.required])],
      lastName:['',Validators.compose([Validators.required])],
      cellPhone:['',Validators.compose([Validators.required])],
      email:['',Validators.compose([Validators.required,Validators.email])],
      password:['',Validators.compose([Validators.required,Validators.minLength(4)])]
    });
  }

  async onRegister(){
    if(!this.registerForm.valid){
        console.log('registration form not valid');
    }    
    let basicProfile = new Registration(
      this.registerForm.get('firstName').value,
      this.registerForm.get('lastName').value,
      this.registerForm.get('email').value,
      this.registerForm.get('email').value,
      this.registerForm.get('password').value,null,false,null,null,null);

    //this.myProfile.setMyProfileRegistration(basicProfile);

    const loading = await this.loadingController.create({
      message:'login in ...'
    });
    loading.present();
    this.myProfile.onRegistration(basicProfile).subscribe(
      (response:Token) => {
        debugger;
          this.myProfile.setUserIdOnLogin(response.user_id);
          this.storageSVC.setStorageValueByKey('access_token',response.access_token);
          this.storageSVC.setStorageValueByKey('refresh_token',response.refresh_token);
          this.myProfile.loadProfile();
          this.router.navigateByUrl('/dashboard');
          loading.dismiss();
      },
      error => {
        console.log(error);
        loading.dismiss();
      }
    );
  }
}
