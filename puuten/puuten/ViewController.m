//
//  ViewController.m
//  puuten
//
//  Created by wang jialei on 12-7-25.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import "ViewController.h"
#import "LoginViewController.h"
@interface ViewController () <LoginViewControllerDelegate>
@property (assign) BOOL login_or_not;
@end

@implementation ViewController
@synthesize imgView;
@synthesize login_or_not;

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    if ([segue.identifier hasPrefix:@"login"]) {
        LoginViewController *login = (LoginViewController *)segue.destinationViewController;
        //login.email = @"email";
        //login.password = @"password";
        login.delegate = self;
    }
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
    NSURL *nsURL = [[NSURL alloc] initWithString:@"http://www.fishjava.com/img/4a0575fc/1a988e79469680d572368.jpg"];
    ASIHTTPRequest *request = [ASIHTTPRequest requestWithURL:nsURL];
    [request setCompletionBlock:^{
        UIImage *image = [[UIImage alloc] initWithData:[request responseData]];
        self.imgView.frame = CGRectMake(0, 0, image.size.width, image.size.height);
        [self.imgView setImage:image];
        
    }];
    [request setFailedBlock:^{
        NSLog(@"%@", @"ppppp");
    }];
    [request startAsynchronous];
}

- (void)viewDidUnload
{
    [self setImgView:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}
- (void)viewDidAppear:(BOOL)animated
{
    if (!login_or_not) {
        [self performSegueWithIdentifier:@"login" sender:self];
    }
    [super viewDidAppear:animated];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
}

- (void)loginViewController:(LoginViewController *)sender 
               login_or_not:(int)userid
{
    self.login_or_not = YES;
    [self dismissModalViewControllerAnimated:YES];
}

@end
