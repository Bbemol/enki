import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { CreateEvenementComponent } from './create-evenement.component';

describe('CreateEvenementComponent', () => {
  let component: CreateEvenementComponent;
  let fixture: ComponentFixture<CreateEvenementComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateEvenementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateEvenementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

/*   it('should create', () => {
    expect(component).toBeTruthy();
  }); */
});
