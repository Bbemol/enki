import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';

import { TOAST_DURATION, ToastComponent } from './toast.component';

describe('ToastComponent', () => {
  let component: ToastComponent;
  let fixture: ComponentFixture<ToastComponent>;

/*   beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ToastComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ToastComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }); */

/*   it('should create', () => {
    expect(component).toBeTruthy();
  }); */

  it('should show toast with error', (done) => {
    const errorMessage = 'Il y a eu une erreur...';
    const toast = new ToastComponent();
    expect(toast.isDisplayed).toBe(false, 'not displayed at first');
    toast.showMessage(errorMessage)
    expect(toast.isDisplayed).toBe(true, 'should be displayed after showing message');
    expect(toast.message).toBe(errorMessage)
    setTimeout(() => {
      expect(toast.isDisplayed).toBe(false, 'toast is hidden after some time');
      done();
    }, TOAST_DURATION)

  })
});
