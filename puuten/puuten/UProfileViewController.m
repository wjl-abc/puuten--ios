//
//  UProfileViewController.m
//  puuten
//
//  Created by wang jialei on 12-7-12.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import "UProfileViewController.h"
#import "UProfile.h"
#import "puutenViewController.h"

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

@interface UProfileViewController ()

@end

@implementation UProfileViewController
@synthesize uProfile = _uProfile;
@synthesize name = _name;
@synthesize about = _about;

- (void)setUProfile:(UProfile *)uProfile{
    if (_uProfile !=uProfile) {
        _uProfile = uProfile;
        [self configureView];
    }
}

- (void)configureView{
    
    if (self.uProfile){
        self.name.text = @"pppppppp";
        self.about.text = @"qqqqqqq";
        
    }
}

- (void)new_conf:(NSData *)responseData{
    NSError* error;
    NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
    NSString* name = [json objectForKey:@"name"];
    NSString* about = [json objectForKey:@"about"];
    self.name.text = name; 
    self.about.text = about;
}

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
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSString *get_profile = [NSString stringWithFormat:@"/profiles/profile/%i/", self.uProfile.userID];
    
    NSURL *editURL = [NSURL URLWithString:get_profile relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:editURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setCompletionBlock:^{
        //NSString *responseString = [request responseString];
        //NSLog(@"Response: %@", responseString);
        NSData *responseData = [request responseData];
        [self new_conf:responseData];
        //NSError* error;
        //NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        
        }];
    [request setFailedBlock:^{
        NSError *error = [request error];
        NSLog(@"Error: %@", error.localizedDescription);
    }];
    
    [request startAsynchronous];

	// Do any additional setup after loading the view.
    [self configureView];
}

- (void)viewDidUnload
{
    [self setName:nil];
    [self setUProfile:nil];
    [self setAbout:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}


@end
