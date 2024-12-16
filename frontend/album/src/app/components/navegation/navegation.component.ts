import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { uploadDialogComponent } from '../../dialog/upload/upload'; 
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-navegation',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './navegation.component.html',
  styleUrls: ['./navegation.component.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class NavegationComponent {
  constructor(private router: Router, public dialog: MatDialog) {}

  goToProfile() {
    this.router.navigate(['/profile']);
  }

  logoutProfile() {
    localStorage.removeItem('token');
    this.router.navigate(['/login']);
  }

  goToUpload() {
    const dialogRef = this.dialog.open(uploadDialogComponent, {
      data: { message: 'Sube tu archivo aquí' }, disableClose: true
    });

    dialogRef.afterClosed().subscribe((result) => {
      if (result) {
        console.log('Upload completed:', result);
      } else {
        console.log('Upload dialog closed');
      }
    });
  }
}