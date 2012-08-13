//
//  BSViewController.h
//  puuten
//
//  Created by wang jialei on 12-8-13.
//
//

#import <UIKit/UIKit.h>

@interface BSViewController : UIViewController
@property (assign, nonatomic) int bs_id;
@property (weak, nonatomic) IBOutlet UIImageView *avatar;
@property (weak, nonatomic) IBOutlet UILabel *name;
@property (weak, nonatomic) IBOutlet UITextView *tags;
@property (weak, nonatomic) IBOutlet UITextView *introduction;

@end