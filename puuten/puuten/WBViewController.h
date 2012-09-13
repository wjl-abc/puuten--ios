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
@property (assign, nonatomic) int bs_id;
@property (assign, nonatomic) int order;
@property (assign, nonatomic) NSMutableArray *arrayData;
@property (weak, nonatomic) NSDictionary *bsdata;
@property (weak, nonatomic) IBOutlet UILabel *bodyField;
@property (strong, nonatomic) IBOutlet UIImageView *pic;
@property (strong, nonatomic) IBOutlet BSHeader *bsHeader;
@property (strong, nonatomic) IBOutlet UILabel *re_wb;
@property (strong, nonatomic) IBOutlet UIView *re_view;

- (IBAction)click:(id)sender;
- (IBAction)go_bs:(id)sender;

@end
