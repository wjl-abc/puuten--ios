//
//  LibViewController.h
//  puuten
//
//  Created by wang jialei on 12-8-17.
//
//

#import <UIKit/UIKit.h>
#import "WaterFlowView.h"
#import "ImageViewCell.h"
#import "Constance.h"

@interface LibViewController : UIViewController<WaterFlowViewDelegate, WaterFlowViewDataSource>
{
    NSMutableArray *arrayData;
    WaterFlowView  *waterFlow;
    int selected_cell;
}

- (void)dataSourceDidLoad;
- (void)dataSourceDidError;

@end
