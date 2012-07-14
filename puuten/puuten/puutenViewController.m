//
//  puutenViewController.m
//  puuten
//
//  Created by wang jialei on 12-7-12.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import "puutenViewController.h"
#import "UProfile.h"
#import "WBViewController.h"

@interface NSDictionary(JSONCategories)
+(NSDictionary*)dictionaryWithContentsOfJSONURLString:(NSString*)urlAddress;
-(NSData*)toJSON;
@end

@implementation NSDictionary(JSONCategories)
+(NSDictionary*)dictionaryWithContentsOfJSONURLString:(NSString*)urlAddress
{
    NSData* data = [NSData dataWithContentsOfURL: [NSURL URLWithString: urlAddress] ];
    __autoreleasing NSError* error = nil;
    id result = [NSJSONSerialization JSONObjectWithData:data options:kNilOptions error:&error];
    if (error != nil) return nil;
    return result;
}

-(NSData*)toJSON
{
    NSError* error = nil;
    id result = [NSJSONSerialization dataWithJSONObject:self options:kNilOptions error:&error];
    if (error != nil) return nil;
    return result;    
}
@end

@interface puutenViewController ()

@end

@implementation puutenViewController
@synthesize loginButton;
@synthesize email;
@synthesize password;
@synthesize userID;

// Send button Touch Up Inside
- (IBAction)login:(id)sender
{
    //NSError* error;
    NSLog(@"%s", __FUNCTION__);
    //Allocate NSURL object
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *loginURL = [NSURL URLWithString:@"/account/login/" relativeToURL:nsURL];
    ASIFormDataRequest* request=[ASIFormDataRequest requestWithURL:loginURL];
    [request setDelegate:self];
    [request setPostValue:email.text forKey:@"username"];
    [request setPostValue:password.text forKey:@"password"];
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request startAsynchronous];
    
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	// Do any additional setup after loading the view, typically from a nib.
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    self.password=nil;
    self.email = nil;
    self.loginButton = nil;
    self.userID = 0;
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
}

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender{
    WBViewController *uProfileController = segue.destinationViewController;
    UProfile *profile = [[UProfile alloc] initWithUserID: self.userID];
    
    uProfileController.uProfile = profile;
}

#pragma mark -
#pragma mark NSURLConnection Callbacks
- ( void )requestFinished:( ASIHTTPRequest *)request
{
    NSString *responseString = [request responseString ]; // 对于 2 进制数据，使用： NSData *responseData = [request responseData];
    NSLog ( @"%@" ,responseString);
    if([responseString intValue]){
        self.userID = [responseString intValue];
        [self performSegueWithIdentifier:@"login" sender:self];
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
