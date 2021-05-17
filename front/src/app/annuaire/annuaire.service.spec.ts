import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs';
import { AnnuaireService } from './annuaire.service';
import { Contact } from '../interfaces/Contact';
import { CONTACTS, ANNUAIRE } from '../mocks/contacts-mocks';
import { HttpClientTestingModule,  HttpTestingController } from '@angular/common/http/testing';

describe('AnnuaireService', () => {
  let annuaireService: AnnuaireService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AnnuaireService],
      imports: [HttpClientTestingModule]
    });
    annuaireService = TestBed.inject(AnnuaireService);
    httpTestingController = TestBed.inject(HttpTestingController);

    

  });

  afterEach(() => {
    httpTestingController.verify();
  });

  it('should be created', () => {
    expect(annuaireService).toBeTruthy();
  });

  describe('all user favs contacts', () => {


    xit('should return favorite contacts of user', () => {
      /* const contactResponse = CONTACTS;
      let response;
      spyOn(annuaireService, 'getUserFavoriteContacts').and.returnValue(of(contactResponse));

      annuaireService.getUserFavoriteContacts().subscribe(res => {
        response = res
      })

      expect(response).toEqual(contactResponse) */
    })
  })
  
  describe('add contact to favorite', () => {
    xit('should add contact to user favs', () => {
      /* const newContact : Contact = ANNUAIRE[2]
      const contactResponse: Contact[] = (CONTACTS as Contact[]).concat(newContact)
      let response;
      spyOn(annuaireService, 'addContactToUserFavs').and.returnValue(of(contactResponse));

      annuaireService.addContactToUserFavs(newContact.uuid).subscribe(res => {
        response = res
      })

      expect(response).toEqual(contactResponse) */
    })
  })

  describe('contact detail', () => {
    xit('should return a contact detail', () => {
      /* const contactResponse = CONTACTS[0];
      let response;
      spyOn(annuaireService, 'getContactDetail').and.returnValue(of(contactResponse));

      annuaireService.getContactDetail('1').subscribe(res => {
        response = res
      })

      expect(response).toEqual(contactResponse) */
    })
  })

  

});
