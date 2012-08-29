//
//  ProfileViewController.h
//  puuten
//
//  Created by wang jialei on 12-8-26.
//
//

#import <UIKit/UIKit.h>
#import "WaterFlowView.h"
#import "ImageViewCell.h"
#import "Constance.h"

@interface ProfileViewController : UIViewController<WaterFlowViewDelegate, WaterFlowViewDataSource>
{
    NSMutableArray *arrayData;
    NSMutableArray *testData;
    WaterFlowView  *waterFlow_wat;
    WaterFlowView  *waterFlow_wish;
    int selected_cell;
}

- (void)dataSourceDidLoad;
- (void)dataSourceDidError;
- (IBAction)click1:(id)sender;
- (IBAction)click2:(id)sender;

@end
