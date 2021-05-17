import { Injectable } from '@angular/core';
import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, UrlTree, ActivatedRoute, Router, PRIMARY_OUTLET } from '@angular/router';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { UserService } from '../user/user.service';
import { REGISTER } from '../constants/constants';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserInfoGuard implements CanActivate {
  constructor(
    private userService: UserService,
    private router: Router
  ) {

  }
  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): Observable<boolean | UrlTree> | Promise<boolean | UrlTree> | boolean | UrlTree {
      // send the first segment of requested route
      const firstSegmentRouterSnapshot = this.router.parseUrl(state.url).root.children[PRIMARY_OUTLET] ? this.router.parseUrl(state.url).root.children[PRIMARY_OUTLET].segments[0].path : ''
      return environment.auth ? this.userIsAuth(firstSegmentRouterSnapshot) : true;
  }

  userIsAuth(firstSegmentRouterSnapshot): Observable<boolean | UrlTree> {
    if (this.userService.userExist) {
      return of(this.getUrlTreeFromCurrentSnapshot(firstSegmentRouterSnapshot))
    } else {
      return this.userService.getUserInfo().pipe(
        map(res => {
          if (res.message === 'success') {
            this.userService.userExist = true;
            // this.userService.user = res.data
            this.userService.user.uuid = res.data.uuid;
            this.userService.user.attributes.fonction = res.data.position.position.slug;
            this.userService.user.fullname = `${res.data.first_name} ${res.data.last_name}`;
            this.userService.user.location = res.data.position.group.location.search_label;
            this.userService.user.location_id = res.data.position.group.location.external_id;

          }
          return this.getUrlTreeFromCurrentSnapshot(firstSegmentRouterSnapshot)
        }
        ),
        catchError(() => {
          return of(this.getUrlTreeFromCurrentSnapshot(firstSegmentRouterSnapshot))
        })
      )
    }
  }
    
  getUrlTreeFromCurrentSnapshot(firstSegmentRouterSnapshot) {
    if (this.userService.userExist) {
      if (firstSegmentRouterSnapshot === 'register') {
        return this.router.parseUrl('/dashboard')
      } else {
        return true
      }
    } else {
      if (firstSegmentRouterSnapshot === REGISTER){
        return true
      } else {
        return this.router.parseUrl(`/${REGISTER}/step1`)
      }
    }
  }
  
}
