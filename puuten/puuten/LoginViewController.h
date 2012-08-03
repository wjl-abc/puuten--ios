//
//  LoginViewController.h
//  puuten
//
//  Created by wang jialei on 12-7-25.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "ASIHTTPRequest.h"
#import "ASIFormDataRequest.h"
#import "Constance.h"
//#define URL @"http://localhost:8000"

@class LoginViewController;
@protocol LoginViewControllerDelegate <NSObject>
- (void)loginViewController:(LoginViewController *)sender
               login_or_not:(int)userid;
@end

@interface LoginViewController : UIViewController
@property (weak, nonatomic) IBOutlet UITextField *emailField;
@property (weak, nonatomic) IBOutlet UITextField *passwordField;
@property (nonatomic, weak) id <LoginViewControllerDelegate> delegate;
- (IBAction)login:(id)sender;

@end
