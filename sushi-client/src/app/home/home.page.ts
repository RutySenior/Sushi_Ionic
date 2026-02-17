import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { SushiService } from '../services/sushi';

@Component({
  selector: 'app-home',
  templateUrl: './home.page.html',
  styleUrls: ['./home.page.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule]
})
export class HomePage implements OnInit {
  // Dati utente
  codiceTavolo: string = '';
  nomeUtente: string = '';
  isLogged: boolean = false;

  // Dati menu e ordini
  prodotti: any[] = [];
  carrello: any[] = [];
  ordiniEffettuati: any[] = [];

  constructor(private sushiService: SushiService) {}

  ngOnInit() {
    this.caricaMenu();
  }

  login() {
    if (this.codiceTavolo.trim() && this.nomeUtente.trim()) {
      this.isLogged = true;
      this.aggiornaStato();
    }
  }

  caricaMenu() {
    this.sushiService.getMenu().subscribe((data: any) => {
      this.prodotti = data;
    });
  }

  aggiungiAlCarrello(prodotto: any) {
    const item = this.carrello.find(p => p.id === prodotto.id);
    if (item) {
      item.quantita++;
    } else {
      this.carrello.push({ ...prodotto, quantita: 1 });
    }
  }

  inviaOrdine() {
    const ordine = {
      codice_tavolo: this.codiceTavolo,
      utente_nome: this.nomeUtente,
      prodotti: this.carrello
    };

    this.sushiService.inviaOrdine(ordine).subscribe(() => {
      alert("Ordine inviato con successo!");
      this.carrello = [];
      this.aggiornaStato();
    });
  }

  aggiornaStato() {
    this.sushiService.getStatoTavolo(this.codiceTavolo).subscribe((data: any) => {
      this.ordiniEffettuati = data;
    });
  }
}