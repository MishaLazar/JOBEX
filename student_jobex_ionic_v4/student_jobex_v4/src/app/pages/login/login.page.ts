import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

  loginForm:FormGroup;
  constructor(public formBuilder: FormBuilder) {
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
  onLogin(){
    console.log(this.loginForm.valid)
    console.log(this.loginForm.value)
}

}
