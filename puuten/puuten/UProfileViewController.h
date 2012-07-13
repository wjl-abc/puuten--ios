//
//  UProfileViewController.h
//  puuten
//
//  Created by wang jialei on 12-7-12.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import <UIKit/UIKit.h>
@class UProfile;

@interface UProfileViewController : UIViewController
@property (strong,nonatomic) UProfile *uProfile;
@property (weak, nonatomic) IBOutlet UILabel *name;

@property (weak, nonatomic) IBOutlet UITextView *about;

@end
