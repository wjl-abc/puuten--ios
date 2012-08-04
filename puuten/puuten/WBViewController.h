//
//  WBViewController.h
//  puuten
//
//  Created by wang jialei on 12-8-3.
//
//

#import <UIKit/UIKit.h>
#import "BSHeader.h"
@interface WBViewController : UIViewController<BSHeaderDelegate>
@property (assign, nonatomic) int wb_id;
@property (weak, nonatomic) NSDictionary *bsdata;
@property (weak, nonatomic) IBOutlet UILabel *name;
@property (weak, nonatomic) IBOutlet UITextView *bodyField;
@property (weak, nonatomic) IBOutlet UIImageView *avatar;


@end
