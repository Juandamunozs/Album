import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { FileUploadService } from '../../service/file-upload.service';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  loginForm: FormGroup;

  constructor(private router: Router, private fileUploadService: FileUploadService) {
    this.loginForm = new FormGroup({
      username: new FormControl('', [Validators.required]),
      password: new FormControl('', [Validators.required])
    });
  }

  // Método para iniciar sesión
  onLogin(): void {
    if (this.loginForm.valid) {
      this.fileUploadService.login(this.loginForm.get('username')?.value, this.loginForm.get('password')?.value).subscribe({
        next: (data) => {
          localStorage.setItem('token', data.token);
          console.log('el token es:', data);
          this.router.navigate(['/home']);
        },
        error: (error) => {
          console.error('Error during login:', error);
          alert('Invalid credentials or server error');
        },
        complete: () => {
          console.log('Login request completed');
        }
      });
    }
  }
}
