//
//  WBCommentViewController.h
//  puuten
//
//  Created by wang jialei on 12-8-14.
//
//

#import <UIKit/UIKit.h>

@interface WBCommentViewController : UIViewController
@property (strong, nonatomic) IBOutlet UITextView *commentField;
- (IBAction)submit:(id)sender;

@end
