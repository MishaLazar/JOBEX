import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { validateConfig } from '@angular/router/src/config';

@Component({
  selector: 'app-register',
  templateUrl: './register.page.html',
  styleUrls: ['./register.page.scss'],
})
export class RegisterPage implements OnInit {
  

  registerForm:FormGroup;
  constructor(public formBuilder: FormBuilder) { 

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

  onRegister(){
    console.log(this.registerForm.valid)
    console.log(this.registerForm.value)
  }
}
