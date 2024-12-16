import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { NavegationComponent } from "../navegation/navegation.component";
import { FileUploadService } from '../../service/file-upload.service';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, NavegationComponent, HttpClientModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  // photos: string[] = [];

  photos: string[] = [];
  photoUrls: string[] = [];

  constructor(private fileUploadService: FileUploadService) { }

  ngOnInit(): void {
    this.loadImages();
  }

  // // Método para cargar las imágenes
  // loadImages(): void {

  //   const token = localStorage.getItem('token');
  //   if (!token) {
  //     console.log('No hay token');
  //     throw new Error('No hay token');
  //   }

  //   this.fileUploadService.getImages().subscribe({
  //     next: (response) => {
  //       this.photos = response.images;
  //       console.log('Fotos cargadas:', this.photos);
  //     },
  //     error: (err) => {
  //       console.error('Error al cargar las imágenes:', err);
  //     },
  //   });
  // }

  // Método para cargar las imágenes
  loadImages(): void {
    this.fileUploadService.getImages().subscribe({
      next: (response) => {
        this.photos = response.images;
        console.log('Fotos cargadas:', this.photos);
        this.loadImageUrls();
      },
      error: (err) => {
        console.error('Error al cargar las imágenes:', err);
      }
    });
  }

  // Método para cargar las imágenes con el token
  loadImageUrls(): void {
    this.photos.forEach(photo => {
      
      console.log(photo);
      
      this.fileUploadService.getImageWithToken(photo).subscribe({
        next: (imageBlob) => {
          const imageUrl = URL.createObjectURL(imageBlob);
          this.photoUrls.push(imageUrl); // Guarda el objeto URL
        },
        error: (err) => {
          console.error('Error al obtener la imagen con token:', err);
        }
      });
    });
  }

  // Metodo para abrir una imagen
  ver(photo: string): void {
    console.log('Ver:', photo);
    window.open(photo, '_blank');
  }

  // Método para eliminar una imagen
  eliminar(photo: string): void {
    console.log('Eliminar:', photo);
    const imageName = photo.split('/uploads/')[1];

    if (imageName) {
      console.log('Nombre de la imagen a eliminar:', imageName);

      this.fileUploadService.deleteImage(imageName).subscribe(
        (response) => {
          console.log('Imagen eliminada con éxito:', response);
          this.loadImages();
        },
        (error) => {
          console.error('Error al eliminar la imagen:', error);
        }
      );
    } else {
      console.error('No se pudo obtener el nombre de la imagen desde la URL.');
    }
  }
}

