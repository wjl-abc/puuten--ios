//
//  UProfileViewController.m
//  puuten
//
//  Created by wang jialei on 12-7-12.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import "WBViewController.h"
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

@interface WBViewController ()

@end

@implementation WBViewController
@synthesize uProfile = _uProfile;
@synthesize locationManager;
@synthesize startLocation;
@synthesize lat=_lat;
@synthesize lng=_lng;
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

- (NSString *)replaceUnicode:(NSString *)unicodeStr {  
    
    NSString *tempStr1 = [unicodeStr stringByReplacingOccurrencesOfString:@"\\u" withString:@"\\U"];  
    NSString *tempStr2 = [tempStr1 stringByReplacingOccurrencesOfString:@"\"" withString:@"\\\""];   
    NSString *tempStr3 = [[@"\"" stringByAppendingString:tempStr2] stringByAppendingString:@"\""];  
    NSData *tempData = [tempStr3 dataUsingEncoding:NSUTF8StringEncoding];  
    NSString* returnStr = [NSPropertyListSerialization propertyListFromData:tempData  
                                                                                 mutabilityOption:NSPropertyListImmutable   
                                                                                           format:NULL  
                                                                                 errorDescription:NULL];  
                          
                          //NSLog(@"Output = %@", returnStr);  
                          
                          return [returnStr stringByReplacingOccurrencesOfString:@"\\r\\n" withString:@"\n"];  
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
    self.locationManager = [[CLLocationManager alloc] init];
    locationManager.desiredAccuracy = kCLLocationAccuracyBest;
    locationManager.delegate = self;
    [locationManager startUpdatingLocation];
    startLocation = nil;
    
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *libURL = [NSURL URLWithString:@"/home/event_lib/" relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:libURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setPostValue:self.lat forKey:@"lat"];
    [request setPostValue:self.lng forKey:@"lng"];
    
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSString *newString = [[NSString alloc] initWithData:responseData encoding:NSASCIIStringEncoding];
        //NSString *responseString = [request responseString];
        NSString *newer = [newString];
        NSLog(@"%@", newString);
    }];
    [request setFailedBlock:^{
        NSError *error = [request error];
        NSLog(@"Error: %@", error.localizedDescription);
    }];
    
    [request startAsynchronous];
    

	// Do any additional setup after loading the view.
    //[self configureView];
}

- (void)viewDidUnload
{
    [self setName:nil];
    [self setUProfile:nil];
    [self setStartLocation:nil];
    [self setLocationManager:nil];
    [self setAbout:nil];
    [self setLat:nil];
    [self setLng:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}


#pragma mark -
#pragma mark CLLocationManagerDelegate

-(void)locationManager:(CLLocationManager *)manager
   didUpdateToLocation:(CLLocation *)newLocation
          fromLocation:(CLLocation *)oldLocation
{
    NSString *currentLatitude = [[NSString alloc] 
                                 initWithFormat:@"%g", 
                                 newLocation.coordinate.latitude];
    self.lat = currentLatitude;
    
    NSString *currentLongitude = [[NSString alloc] 
                                  initWithFormat:@"%g",
                                  newLocation.coordinate.longitude];
    self.lng = currentLongitude;
}
-(void)locationManager:(CLLocationManager *)manager 
      didFailWithError:(NSError *)error
{
}


@end
