import { Component, Inject } from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatDialogModule } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';
import { FileUploadService } from '../../service/file-upload.service'; 

@Component({
  selector: 'app-upload-dialog',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatDialogModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule
  ],
  templateUrl: './upload.html',
  styleUrls: ['./upload.css']
})
export class uploadDialogComponent {
  uploadForm: FormGroup;
  selectedFile: File | null = null;

  constructor(
    private fb: FormBuilder,
    public dialogRef: MatDialogRef<uploadDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { message: string },
    private fileUploadService: FileUploadService 
  ) {
    this.uploadForm = this.fb.group({
      title: ['', [Validators.required]],
    });
  }

  onFileSelected(event: any) {
    const file = event.target.files[0];
    this.selectedFile = file;
    console.log('Selected file:', this.selectedFile);
  }

  cerrar() {
    this.dialogRef.close();
  }

  onSubmit() {
    if (this.uploadForm.valid && this.selectedFile) {
      const formData = new FormData();
      formData.append('title', this.uploadForm.get('title')?.value);
      formData.append('file', this.selectedFile);


      this.fileUploadService.uploadFile(formData).subscribe({
          next: (response: any) => {
            console.log('Archivo subido con éxito', response);
            this.dialogRef.close({success: true, response: response}); 
          },
          error: (error: any) => {
            console.error('Error al subir el archivo', error);
            this.dialogRef.close({success: false, error: error}); 
          }
        });

    } else {
      console.log('Formulario invalido o no tiene archivo seleccionado');
    }
  }
}