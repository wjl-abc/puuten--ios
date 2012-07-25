//
//  LoginViewController.m
//  puuten
//
//  Created by wang jialei on 12-7-25.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import "LoginViewController.h"

@interface LoginViewController ()

@end

@implementation LoginViewController
@synthesize emailField;
@synthesize passwordField;
@synthesize delegate;

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view.
}

- (void)viewDidUnload
{
    [self setEmailField:nil];
    [self setPasswordField:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (IBAction)login:(id)sender {
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *loginURL = [NSURL URLWithString:@"/account/login/" relativeToURL:nsURL];
    ASIFormDataRequest* request=[ASIFormDataRequest requestWithURL:loginURL];
    [request setDelegate:self];
    [request setPostValue:emailField.text forKey:@"username"];
    [request setPostValue:passwordField.text forKey:@"password"];
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request startAsynchronous];
}

- ( void )requestFinished:( ASIHTTPRequest *)request
{
    NSString *responseString = [request responseString ]; // 对于 2 进制数据，使用： NSData *responseData = [request responseData];
    if([responseString intValue]){
        //[[self presentingViewController] dismissModalViewControllerAnimated:YES];
        [self.delegate loginViewController:self login_or_not:[responseString intValue]];
    }
    else {
        NSLog(@"you are a fool");
    }
    
}
// 请求失败，获取 error
- ( void )requestFailed:( ASIHTTPRequest *)request
{
    NSError *error = [request error ];
    NSLog ( @"%@" ,error. userInfo );
    
}
@end
