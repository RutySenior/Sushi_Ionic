import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { StaffService } from './services/staff';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App implements OnInit {
  ordini: any[] = [];
  prodotti: any[] = [];
  categorie: any[] = [];

  // Form per nuovo prodotto
  nuovoProdotto = { nome: '', prezzo: 0, immagine_url: '', categoria_id: 1 };

  constructor(private staffService: StaffService) {}

  ngOnInit() {
    this.caricaDati();
  }

  caricaDati() {
    this.staffService.getTuttiOrdini().subscribe(data => this.ordini = data);
    this.staffService.getMenu().subscribe(data => this.prodotti = data);
    this.staffService.getCategorie().subscribe(data => this.categorie = data);
  }

  cambiaStato(id: number, stato: string) {
    this.staffService.aggiornaStato(id, stato).subscribe(() => this.caricaDati());
  }

  aggiungiPiatto() {
    this.staffService.aggiungiProdotto(this.nuovoProdotto).subscribe(() => {
      alert("Piatto aggiunto!");
      this.caricaDati();
    });
  }

  eliminaPiatto(id: number) {
    if(confirm("Eliminare questo piatto?")) {
      this.staffService.eliminaProdotto(id).subscribe(() => this.caricaDati());
    }
  }
}