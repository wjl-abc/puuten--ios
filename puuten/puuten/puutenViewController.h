//
//  puutenViewController.h
//  puuten
//
//  Created by wang jialei on 12-7-12.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import "ASIHTTPRequest.h"
#import "ASIFormDataRequest.h"
#define URL @"http://localhost:8000"

@interface puutenViewController : UIViewController{
    UIButton *loginButton;
    UITextField *email;
    UITextField *password;
    int userID;
}

@property (nonatomic, retain) IBOutlet UIButton *loginButton;
@property (nonatomic, retain) IBOutlet UITextField *email;
@property (nonatomic, retain) IBOutlet UITextField *password;
@property (assign) int userID;

- (IBAction)login:(id)sender;

@end
