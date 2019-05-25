import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';
import { AuthenticationGuardGuard } from './guards/authentication-guard.guard';

const routes: Routes = [
  { path: '', redirectTo: '/my-profile', pathMatch: 'full' },
  // { path: 'home', loadChildren: './pages/home/home.module#HomePageModule' },
  { path: 'login', loadChildren: './pages/login/login.module#LoginPageModule' },
  { path: 'register', loadChildren: './pages/register/register.module#RegisterPageModule' },
  { path: 'my-profile', loadChildren: './pages/my-profile/my-profile.module#MyProfilePageModule',canLoad:[AuthenticationGuardGuard] },
  { path: 'dashboard', loadChildren: './pages/dashboard/dashboard.module#DashboardPageModule',canLoad:[AuthenticationGuardGuard] },
  { path: 'dashboard/engagement/:matchId', loadChildren: './pages/engagement/engagement.module#EngagementPageModule',canLoad:[AuthenticationGuardGuard]},
  { path: 'my-profile/engagements-list/engagement/:matchId', loadChildren: './pages/engagement/engagement.module#EngagementPageModule',canLoad:[AuthenticationGuardGuard] },
  { path: 'my-profile/engagements-list', loadChildren: './pages/engagements-list/engagements-list.module#EngagementsListPageModule',canLoad:[AuthenticationGuardGuard] },
  { path: 'my-profile/personal-data', loadChildren: './pages/personal-data/personal-data.module#PersonalDataPageModule',canLoad:[AuthenticationGuardGuard] },
  { path: 'my-profile/skills', loadChildren: './pages/skills/skills.module#SkillsPageModule',canLoad:[AuthenticationGuardGuard] },
  { path: 'my-profile/wish-list', loadChildren: './pages/wish-list/wish-list.module#WishListPageModule' ,canLoad:[AuthenticationGuardGuard]},  
  { path: 'my-profile/cities', loadChildren: './pages/cities/cities.module#CitiesPageModule',canLoad:[AuthenticationGuardGuard] },






];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { preloadingStrategy: PreloadAllModules })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
