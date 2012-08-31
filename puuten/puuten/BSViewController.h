//
//  BSViewController.h
//  puuten
//
//  Created by wang jialei on 12-8-5.
//
//

#import <UIKit/UIKit.h>
#import "WaterFlowView.h"
#import "ImageViewCell.h"

@interface BSViewController : UIViewController<WaterFlowViewDelegate, WaterFlowViewDataSource>
{
    NSMutableArray *arrayData;
    WaterFlowView  *waterFlow_self;
    WaterFlowView  *waterFlow_others;
    int selected_cell;
}
@property (assign, nonatomic) int bs_id;
@property (weak, nonatomic) IBOutlet UIImageView *avatar;
@property (weak, nonatomic) IBOutlet UILabel *name;
@property (weak, nonatomic) IBOutlet UITextView *tags;
@property (weak, nonatomic) IBOutlet UITextView *introduction;

@property (strong, nonatomic) IBOutlet UIButton *selfButton;
@property (strong, nonatomic) IBOutlet UIButton *othersButton;
- (void)dataSourceDidLoad;
- (void)dataSourceDidError;
- (IBAction)click1:(id)sender;
- (IBAction)click2:(id)sender;

@end
