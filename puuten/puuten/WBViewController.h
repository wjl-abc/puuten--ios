//
//  UProfileViewController.h
//  puuten
//
//  Created by wang jialei on 12-7-12.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <CoreLocation/CoreLocation.h>
@class UProfile;

@interface WBViewController : UIViewController<CLLocationManagerDelegate>{
    CLLocationManager *locationManager;
    CLLocation *startLocation;
}
@property (strong,nonatomic) UProfile *uProfile;
@property (strong,nonatomic) CLLocationManager *locationManager;
@property (strong,nonatomic) CLLocation *startLocation;
@property (weak, nonatomic) NSString *lat;
@property (weak, nonatomic) NSString *lng;
@property (weak, nonatomic) IBOutlet UILabel *name;
@property (weak, nonatomic) IBOutlet UITextView *about;

@end
